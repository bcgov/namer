import 'reflect-metadata';
import 'zone.js';

import { enableProdMode } from '@angular/core';

import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { NamerModuleNgFactory } from './aot/namer/namer.module.ngfactory';

enableProdMode();
platformBrowserDynamic().bootstrapModuleFactory(NamerModuleNgFactory);

