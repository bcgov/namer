//import 'zone.js';

import 'zone.js/dist/zone';
import 'reflect-metadata';

import { enableProdMode } from '@angular/core';

import { platformBrowser } from '@angular/platform-browser';

import { NamerModuleNgFactory } from './aot/namer/namer.module.ngfactory';

enableProdMode();
platformBrowser().bootstrapModuleFactory(NamerModuleNgFactory);

