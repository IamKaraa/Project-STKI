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
                $response = Http::timeout(10)->get($apiUrl, [
                    'q' => $query
                ]);

                if ($response->successful()) {
                    $data = $response->json();
                    $results = $data['data'] ?? [];
                    $total_hasil = $data['total_hasil'] ?? 0;
                }
            } catch (\Exception $e) {
                return back()->with('error', 'Gagal terhubung ke mesin pencari.');
            }
        }

        return view('search', compact('results', 'query', 'total_hasil'));
    }

    public function showAll()
    {
        $results = [];
        $total_hasil = 0;
        
        $apiUrl = 'https://project-stki.vercel.app/search'; 
        
        try {
            $response = Http::timeout(10)->get($apiUrl);

            if ($response->successful()) {
                $data = $response->json();
                $results = $data['data'] ?? [];
                $total_hasil = $data['total'] ?? 0;
            }
        } catch (\Exception $e) {
            return back()->with('error', 'Gagal terhubung ke mesin pencari API.');
        }

        // Kita manipulasi variabel $query agar tampilan tetap merender daftarnya
        $query = "Semua Dokumen dalam Sistem";
        
        return view('search', compact('results', 'query', 'total_hasil'));
    }
}