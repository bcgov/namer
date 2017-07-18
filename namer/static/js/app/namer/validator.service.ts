import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';


export class ValidationResult {
    corporation: CorporationResult;
    descriptive: DescDistObj;
    distinct: DescDistObj;
}

class CorporationResult {
    errors: ErrorsObj[];
    valid: boolean;
}

class DescDistObj {
    errors: ErrorsObj[];
    exists: boolean;
    value: string;
}

class ErrorsObj {
    code: number;
    message: string;
    severity: number;
}

@Injectable()
export class ValidatorService {
    private validatorUrl = '/api/validator/v1'; //root url

    constructor (private http: Http) {}

    validate(corpName: string): Observable<ValidationResult[]> {
        let url = this.validatorUrl + "/validate";
        let postBody = {name: corpName};

        return this.http.post(url, postBody)
                    .map(this.extractData)
                    .catch(this.handleError);
    }

    private extractData(res: Response) {
        var hitResults: ValidationResult[] = JSON.parse(res.text());
        return hitResults;
    }

    private handleError (error: Response | any) {
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }
}