<?php
$lockFile = '/home/i/ivtru1ym/ivtru1ym.beget.tech/public_html/643_bot_GPT/643_bot.lock';
if (file_exists($lockFile)) {
    unlink($lockFile);
}
exec('python3 /home/i/ivtru1ym/ivtru1ym.beget.tech/public_html/643_bot_GPT/643_bot.py >> /home/i/ivtru1ym/ivtru1ym.beget.tech/public_html/643_bot_GPT/cron.log 2>&1');
?>