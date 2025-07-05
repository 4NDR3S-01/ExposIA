<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class Notifier
{
    public function send(string $event, array $payload): void
    {
        Http::withToken(config('services.ws.token'))
            ->post(rtrim(config('services.ws.url'), '/').'/notify', [
                'event'   => $event,
                'payload' => $payload,
            ]);
    }
}
