FROM seegno/bitcoind

COPY data/bitcoin.conf /root/.bitcoin/bitcoin.conf
COPY data/bitcoin.conf /opt/bitcoin/bitcoind.conf
RUN apt update && apt install -y net-tools procps
