<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class SearchController extends Controller
{
    public function index(Request $request)
    {
        $query = $request->input('q');
        $results = [];
        $total_hasil = 0;

        if ($query) {
            $apiUrl = 'https://project-stki.vercel.app/search'; 
            
            try {
            if ($query) {
                // Jika user melakukan pencarian
                $response = Http::timeout(10)->get($apiUrl . '/search', [
                    'q' => $query
                ]);
                
                if ($response->successful()) {
                    $data = $response->json();
                    $results = $data['data'] ?? [];
                    $total_hasil = $data['total_hasil'] ?? 0;
                }
            } else {
                // Jika user baru membuka halaman (Dashboard)
                $response = Http::timeout(10)->get($apiUrl . '/all-documents');
                
                if ($response->successful()) {
                    $data = $response->json();
                    $results = $data['data'] ?? [];
                    // Rute all-documents menggunakan key 'total', bukan 'total_hasil'
                    $total_hasil = $data['total'] ?? 0; 
                }
            }
        } catch (\Exception $e) {
            return view('search', compact('results', 'query', 'total_hasil'))
                   ->with('error', 'Gagal terhubung ke mesin pencari API.');
        }

        return view('search', compact('results', 'query', 'total_hasil'));
        }
    }
}