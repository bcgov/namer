import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { NamerService, HitResult } from './namer.service.js';
import { ValidatorService, ValidationResult } from './validator.service.js';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';

@Component({
    selector: 'namer',
    templateUrl: '/static/js/app/namer/namer.template.html',
    providers: [NamerService, ValidatorService]
})

export class NamerComponent {

    ERROR_CLASS = "validationError";
    WARN_CLASS = "validationWarn";

    searchBox: FormControl;
    options: any;

    validating: boolean;
    showValidation: boolean;
    distinct: string;
    distinctErrors: string;
    distinctErrorClass: string;
    descriptive: string;
    descriptiveErrors: string;
    descriptiveErrorClass: string;
    corporate: string;
    corporateErrors: string;
    corporateErrorClass: string;
    fullSearchResults: string;
    validateEnabled: boolean;

    constructor(private namerService : NamerService, private validatorService: ValidatorService) {
        this.searchBox = new FormControl();
        this.showValidation = false;
        this.validateEnabled = false;
        this.validating = false;
        this.searchBox.valueChanges.subscribe(
            data => this.getHits(data)
        )
    }

    getHits(val: string) {
        if (val.length < 3 ){
            this.options = [];
            this.validateEnabled = false;
            return;
        }

        let splitted = val.replace(/\s+/g,' ').trim().split(' ');
        this.validateEnabled = ( (splitted.length > 2) && (splitted[2].length > 0) && (this.validating == false));

        this.namerService.getHits(val).subscribe(
            data => this.options = data.hits ? data.hits : []
        );
    }

    highlight(val: string){
        let value = this.searchBox.value.toUpperCase();
        let mark = "<mark>" + value + "</mark>";
        val = val.replace(value, mark);

        return val;
    }

    check(){
        let val = this.searchBox.value;
        this.validating = true;
        this.showValidation = true;
        this.distinct = "";
        this.distinctErrors = "";
        this.distinctErrorClass = "";
        this.descriptive = "";
        this.descriptiveErrors = "";
        this.descriptiveErrorClass = "";
        this.corporate = "";
        this.corporateErrors = "";
        this.corporateErrorClass = "";
        this.fullSearchResults = "";

        let done = 0;

        this.validatorService.validate(this.searchBox.value).subscribe(
            (data) => {
                console.log(data);
                this.distinct = data.distinct.value;
                if ( data.distinct.errors.errors[0] ) {
                    this.distinctErrors = data.distinct.errors.errors[0].message;
                    console.log("distinct severity: " + data.distinct.errors.errors[0].severity);
                    console.log("distinct error: " + data.distinct.errors.SEVERITY_ERROR_VALUE);
                    console.log("distinct warn: " + data.distinct.errors.SEVERITY_WARN_VALUE);
                    this.distinctErrorClass = (data.distinct.errors.errors[0].severity == data.distinct.errors.SEVERITY_ERROR_VALUE) ? this.ERROR_CLASS :
                                             ( (data.distinct.errors.errors[0].severity == data.distinct.errors.SEVERITY_WARN_VALUE) ? this.WARN_CLASS : "" );
                }

                this.descriptive = data.descriptive.value;
                if ( data.descriptive.errors.errors[0] ) {
                    this.descriptiveErrors = data.descriptive.errors.errors[0].message;
                    this.descriptiveErrorClass = (data.descriptive.errors.errors[0].severity == data.descriptive.errors.SEVERITY_ERROR_VALUE) ? this.ERROR_CLASS :
                                             ( (data.descriptive.errors.errors[0].severity == data.descriptive.errors.SEVERITY_WARN_VALUE) ? this.WARN_CLASS : "" );
                }

                this.corporate = data.corporation.value;
                if ( data.corporation.errors.errors[0] ) {
                    this.corporateErrors = data.corporation.errors.errors[0].message;
                    this.corporateErrorClass = (data.corporation.errors.errors[0].severity == data.corporation.errors.SEVERITY_ERROR_VALUE) ? this.ERROR_CLASS :
                                             ( (data.corporation.errors.errors[0].severity == data.corporation.errors.SEVERITY_WARN_VALUE) ? this.WARN_CLASS : "" );
                }

                done++;
                if (done == 2){
                    this.validating = false;
                    let splitted = val.replace(/\s+/g,' ').trim().split(' ');
                    this.validateEnabled = ( (splitted.length > 2) && (splitted[2].length > 0) && (this.validating == false));
                }
            }
        );

        this.namerService.getHits(this.searchBox.value).subscribe(
            (data) => {
                let results = "";
                for (var i=0; i<data.hits.length; i++){
                    let div = "<div>"+data.hits[i].label+"</div>";
                    results += div;
                }
                done++;
                if (done == 2){
                    this.validating = false;
                    let splitted = val.replace(/\s+/g,' ').trim().split(' ');
                    this.validateEnabled = ( (splitted.length > 2) && (splitted[2].length > 0) && (this.validating == false));
                }
                this.fullSearchResults = results;
            }
        );
    }
}