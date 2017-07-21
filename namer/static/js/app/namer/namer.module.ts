import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { MdInputModule, MdAutocompleteModule } from '@angular/material';
import { HttpModule, JsonpModule } from '@angular/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { NamerComponent } from './namer.component';

@NgModule({
    imports:      [
                    BrowserModule,
                    BrowserAnimationsModule,
                    FormsModule,
                    HttpModule,
                    JsonpModule,
                    ReactiveFormsModule,
                    MdInputModule,
                    MdAutocompleteModule
                  ],
    declarations: [ NamerComponent ],
    bootstrap:    [ NamerComponent ],
})
export class NamerModule { }