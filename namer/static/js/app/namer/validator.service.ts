import { Injectable } from '@angular/core';
import { Http, RequestOptions, Response, URLSearchParams } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';


export class ValidationResult {
    corporation: CorporationResult;
    descriptive: DescDistObj;
    distinct: DescDistObj;
}

class CorporationResult {
    errors: ErrorsObj;
    valid: boolean;
    value: string;
}

class DescDistObj {
    errors: ErrorsObj;
    exists: boolean;
    value: string;
}

class ErrorsObj {
    SEVERITY_WARN_VALUE: number;
    SEVERITY_ERROR_VALUE: number;
    errors: ErrorsArr[]
}

class ErrorsArr{
    code: number;
    message: string;
    severity: number;
}

@Injectable()
export class ValidatorService {
    private validatorUrl = '/api/validator/v1'; //root url

    constructor (private http: Http) {}

    validate(query: string): Observable<ValidationResult> {
        let url = this.validatorUrl + "/validate";

        let params: URLSearchParams = new URLSearchParams();
        params.set('q', query);

        let requestOptions = new RequestOptions();
        requestOptions.search = params;

        return this.http.get(url, requestOptions)
                    .map(this.extractData)
                    .catch(this.handleError);
    }

    private extractData(res: Response) {
        var result = JSON.parse(res.text());
        var validationResults: ValidationResult = result;
        return validationResults;
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