FROM seegno/bitcoind

COPY config/bitcoin.conf /root/.bitcoin/bitcoin.conf
COPY config/bitcoin.conf /opt/bitcoin/bitcoind.conf
RUN apt update && apt install -y net-tools procps
