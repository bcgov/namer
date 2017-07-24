import { Component, ChangeDetectorRef} from '@angular/core';
import { FormControl } from '@angular/forms';
import { NamerService, HitResult } from './namer.service';
import { ValidatorService, ValidationResult } from './validator.service';

@Component({
    selector: 'namer',
    templateUrl: './namer.template.html',
    host: {
        '(document:keydown)': 'keymonitor($event)'
    },
    providers: [NamerService, ValidatorService]
})

export class NamerComponent {

    ERROR_CLASS = "validationError";
    WARN_CLASS = "validationWarn";
    PASS_CLASS = "validationPassed";

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

    constructor(private namerService : NamerService, private validatorService: ValidatorService, private changeDetector: ChangeDetectorRef) {
        this.searchBox = new FormControl();
        this.showValidation = false;
        this.validateEnabled = false;
        this.validating = false;
        this.searchBox.valueChanges.subscribe(
            data =>  this.getHits(data)
        )
    }

    keymonitor(event: any){
        if ((event.keyCode == 13) && (this.validateEnabled) && (!this.validating) ){
            this.check();
        }
        console.log("Key press - Triggering change");
        this.changeDetector.detectChanges();
    }

    getHits(val: string) {
        if (val.length < 2 ){
            this.options = [];
            this.validateEnabled = false;
            return;
        }

        let splitted = val.replace(/\s+/g,' ').trim().split(' ');
        this.validateEnabled = ( (splitted.length > 2) && (splitted[2].length > 0) && (this.validating == false));

        this.namerService.getHits(val).subscribe(
            (data) => {
                this.options = data.hits ? data.hits : [];
                this.changeDetector.detectChanges();
            }
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
        this.distinctErrorClass = this.PASS_CLASS;
        this.descriptive = "";
        this.descriptiveErrors = "";
        this.descriptiveErrorClass = this.PASS_CLASS;
        this.corporate = "";
        this.corporateErrors = "";
        this.corporateErrorClass = this.PASS_CLASS;
        this.fullSearchResults = "";

        let done = 0;

        this.validatorService.validate(this.searchBox.value).subscribe(
            (data) => {
                this.distinct = data.distinct.value;
                this.distinctErrors = "";
                for (var i=0; i<data.distinct.errors.errors.length; i++){
                    this.distinctErrors += "<div>" + data.distinct.errors.errors[i].message + "</div>";
                    this.distinctErrorClass = (data.distinct.errors.errors[i].severity == data.distinct.errors.ERROR_VALUE) ? this.ERROR_CLASS :
                                             ( (data.distinct.errors.errors[i].severity == data.distinct.errors.WARN_VALUE) ? this.WARN_CLASS : this.PASS_CLASS );
                }

                this.descriptive = data.descriptive.value;
                this.descriptiveErrors = "";
                for (var i=0; i<data.descriptive.errors.errors.length; i++){
                    this.descriptiveErrors += "<div>" + data.descriptive.errors.errors[i].message + "</div>";
                    this.descriptiveErrorClass = (data.descriptive.errors.errors[i].severity == data.descriptive.errors.ERROR_VALUE) ? this.ERROR_CLASS :
                                             ( (data.descriptive.errors.errors[i].severity == data.descriptive.errors.WARN_VALUE) ? this.WARN_CLASS : this.PASS_CLASS );
                }

                this.corporate = data.corporation.value;
                this.corporateErrors = "";
                for (var i=0; i<data.corporation.errors.errors.length; i++){
                    this.corporateErrors += "<div>" + data.corporation.errors.errors[i].message + "</div>";
                    this.corporateErrorClass = (data.corporation.errors.errors[i].severity == data.corporation.errors.ERROR_VALUE) ? this.ERROR_CLASS :
                                             ( (data.corporation.errors.errors[i].severity == data.corporation.errors.WARN_VALUE) ? this.WARN_CLASS : this.PASS_CLASS );
                }

                done++;
                if (done == 2){
                    this.validating = false;
                    let splitted = val.replace(/\s+/g,' ').trim().split(' ');
                    this.validateEnabled = ( (splitted.length > 2) && (splitted[2].length > 0) && (this.validating == false));
                }
                this.changeDetector.detectChanges();
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
                this.changeDetector.detectChanges();
            }
        );
    }
}
