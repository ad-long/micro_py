cd email && tmux new-session -d -s email_8000 \; send-keys "gunicorn --bind 0.0.0.0:8000 wsgi:app" Enter && cd ..
cd usa_futures/index && tmux new-session -d -s nq_8010 \; send-keys "gunicorn --bind 0.0.0.0:8010 wsgi:app" Enter && cd ../..
cd agu/code && tmux new-session -d -s agu_code_8020 \; send-keys "gunicorn --bind 0.0.0.0:8020 wsgi:app" Enter && cd ../..
cd agu/kline && tmux new-session -d -s agu_kline_8021 \; send-keys "gunicorn --bind 0.0.0.0:8021 wsgi:app" Enter && cd ../..
cd agu/net_flow && tmux new-session -d -s agu_net_flow_8022 \; send-keys "gunicorn --bind 0.0.0.0:8022 wsgi:app" Enter && cd ../..
cd agu/trade_info && tmux new-session -d -s agu_trade_info_8023 \; send-keys "gunicorn --bind 0.0.0.0:8023 wsgi:app" Enter && cd ../..
