// 6 Janeiro 2026 00:00:01 Brazil Time (UTC-3)
        const end = new Date('2026-01-06T00:00:01-03:00').getTime();

        function upd() {
            const now = new Date().getTime();
            const diff = end - now;

            if (diff < 0) {
                clearInterval(int);
                document.getElementById('countdown').innerHTML = '<div style="grid-column:1/-1;text-align:center;font-size:28px;font-weight:900;background:linear-gradient(135deg,#ffd700,#ff6f00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">🎉 LANÇADO! 🎉</div>';
                return;
            }

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hrs = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const secs = Math.floor((diff % (1000 * 60)) / 1000);

            document.getElementById('d').textContent = String(days).padStart(2, '0');
            document.getElementById('h').textContent = String(hrs).padStart(2, '0');
            document.getElementById('m').textContent = String(mins).padStart(2, '0');
            document.getElementById('s').textContent = String(secs).padStart(2, '0');
        }

        upd();
        const int = setInterval(upd, 1000);