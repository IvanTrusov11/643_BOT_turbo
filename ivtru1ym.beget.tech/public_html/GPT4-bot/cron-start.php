<?php
$lockFile = '/home/i/ivtru1ym/ivtru1ym.beget.tech/public_html/GPT4-bot/643_bot.lock';
if (file_exists($lockFile)) {
    unlink($lockFile);
}
exec('python3 /home/i/ivtru1ym/ivtru1ym.beget.tech/public_html/GPT4-bot/main.py >> /home/i/ivtru1ym/ivtru1ym.beget.tech/public_html/GPT4-bot/cron.log 2>&1');
?>


../ivtru1ym.beget.tech/public_html/GPT4-bot/main.py