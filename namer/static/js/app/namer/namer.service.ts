import { Injectable } from '@angular/core';
import { Http, RequestOptions, Response, URLSearchParams } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';


export class HitResult {
    hits: Hit[];
}

class Hit {
    label: string;
    value: string;
    id: string;
}

@Injectable()
export class NamerService {
    private namerUrl = '/api/search/v1/search';  // URL to web API

    constructor (private http: Http) {}

    getHits(query: string): Observable<HitResult> {
        let limit = 20;

        let params: URLSearchParams = new URLSearchParams();
            params.set('q', query);
            params.set('limit', limit.toString());

        let requestOptions = new RequestOptions();
        requestOptions.search = params;

        return this.http.get(this.namerUrl, requestOptions)
                    .map(this.extractData)
                    .catch(this.handleError);
    }

    private extractData(res: Response) {
        var hitResults: HitResult[] = JSON.parse(res.text());
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
