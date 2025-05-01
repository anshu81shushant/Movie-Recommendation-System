mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = fasle\n\
headleess = true\n\
\n\
" > ~/.streamlit/config.toml