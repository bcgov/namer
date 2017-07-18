import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
import { NamerService, HitResult } from './namer.service.js';

import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/map';

@Component({
    selector: 'namer',
    templateUrl: '/static/js/app/namer/namer.template.html',
    providers: [NamerService]
})

export class NamerComponent {

    searchBox: FormControl;
    options: any;
    errorMessage: any;

    constructor(private namerService : NamerService) {
      this.searchBox = new FormControl();
      this.searchBox.valueChanges.subscribe(
          data => this.getHits(data)
      )
   }

   getHits(val: string) {
        this.namerService.getHits(val).subscribe(
            data => this.options = data
        );
   }

}