import {enableProdMode} from '@angular/core';

import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { NamerModule } from './namer/namer.module.js';

enableProdMode();
platformBrowserDynamic().bootstrapModule(NamerModule);

