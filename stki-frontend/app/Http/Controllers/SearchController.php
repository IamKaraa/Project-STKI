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
            // Ganti URL di bawah ini dengan URL publik Vercel milikmu
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
                // Tangani error jika API sedang down atau timeout
                return back()->with('error', 'Gagal terhubung ke mesin pencari.');
            }
        }

        return view('search', compact('results', 'query', 'total_hasil'));
    }
}