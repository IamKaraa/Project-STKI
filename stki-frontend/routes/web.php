<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SearchController;

Route::get('/', [SearchController::class, 'index'])->name('home');
Route::get('/all-documents', [SearchController::class, 'showAll'])->name('all.documents');