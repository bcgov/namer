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

    searchBox: FormControl;
    options: any;

    showValidation: boolean;
    distinct: string;
    distinctErrors: string;
    descriptive: string;
    descriptiveErrors: string;
    corporate: string;
    corporateErrors: string;
    fullSearchResults: string;

    constructor(private namerService : NamerService, private validatorService: ValidatorService) {
      this.searchBox = new FormControl();
      this.showValidation = false;
      this.searchBox.valueChanges.subscribe(
          data => this.getHits(data)
      )
    }

    getHits(val: string) {
        if (val.length < 3 ){
            this.options = [];
            return;
        }

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
        this.showValidation = true;
        this.distinct = "";
        this.distinctErrors = "";
        this.descriptive = "";
        this.descriptiveErrors = "";
        this.corporate = "";
        this.corporateErrors = "";
        this.fullSearchResults = "";

        this.validatorService.validate(this.searchBox.value).subscribe(
            data => function(data: any){
                this.distinct = data.distinct.value;
                this.distinctErrors = data.distinct.errors[0] ? data.distinct.errors[0].message : "";
                this.descriptive = data.descriptive.value;
                this.descriptiveErrors = data.descriptive.errors[0] ? data.descriptive.errors[0].message : "";
                this.corporate = data.corporation.value;
                this.corporateErrors = data.descriptive.errors[0] ? data.descriptive.errors[0].message : "";
            }
        )

        this.namerService.getHits(this.searchBox.value).subscribe(
            data => function(data: any){
                this.fullSearchResults = data.hits ? data.hits : "";
            }
        );
    }

}