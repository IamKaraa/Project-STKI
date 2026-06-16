<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mesin Pencari Jaminan Sosial</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .search-container { margin-top: 10vh; margin-bottom: 5vh; transition: margin 0.3s ease; }
        .search-container.has-results { margin-top: 3vh; }
        .result-card { border-left: 4px solid #0d6efd; transition: transform 0.2s; }
        .result-card:hover { transform: translateX(5px); }
        .score-badge { font-size: 0.85em; }
    </style>
</head>
<body>

<div class="container">
    <div class="row justify-content-center search-container {{ isset($query) && $query ? 'has-results' : '' }}">
        <div class="col-md-8 text-center">
            <h2 class="mb-4 text-primary fw-bold">STKI Search</h2>
            <form action="{{ route('home') }}" method="GET" class="d-flex shadow-sm rounded">
                <input type="text" name="q" class="form-control form-control-lg border-0" 
                       placeholder="Cari dokumen regulasi ketenagakerjaan, JHT, JKK..." 
                       value="{{ $query ?? '' }}">
                <button type="submit" class="btn btn-primary btn-lg px-4 border-0">Cari</button>
            </form>
            
            <div class="mt-3">
                <a href="{{ route('all.documents') }}" class="btn btn-outline-secondary btn-sm">Lihat Semua Dokumen</a>
            </div>
        </div>
    </div>

    @if(session('error'))
        <div class="alert alert-danger text-center">{{ session('error') }}</div>
    @endif

    @if(isset($query) && $query)
        <div class="row justify-content-center">
            <div class="col-md-8">
                <p class="text-muted mb-4">Menemukan {{ $total_hasil ?? 0 }} hasil untuk <strong>"{{ $query }}"</strong></p>

                @forelse($results ?? [] as $item)
                    <div class="card mb-3 border-0 shadow-sm result-card">
                        <div class="card-body">
                            <h5 class="card-title text-primary mb-1">
                                <a href="{{ $item['url_sumber'] }}" target="_blank" class="text-decoration-none">
                                    {{ $item['judul'] }}
                                </a>
                            </h5>
                            @if(isset($item['skor_relevansi']))
                                <span class="badge bg-success mb-2 score-badge">Skor Relevansi: {{ $item['skor_relevansi'] }}</span>
                            @else
                                <span class="badge bg-secondary mb-2 score-badge">Dokumen Sistem</span>
                            @endif
                            <p class="card-text text-muted mb-2">{{ isset($item['konten_snippet']) ? $item['konten_snippet'] : substr($item['konten'], 0, 120) . '...' }}</p>
                            <small class="text-primary">{{ $item['url_sumber'] }}</small>
                        </div>
                    </div>
                @empty
                    <div class="text-center mt-5">
                        <h5 class="text-muted">Tidak ada dokumen yang ditemukan.</h5>
                    </div>
                @endforelse
            </div>
        </div>
    @endif
</div>

</body>
</html>