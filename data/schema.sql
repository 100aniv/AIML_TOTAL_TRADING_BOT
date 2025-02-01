-- schema.sql
-- 데이터베이스 스키마 정의

-- OHLCV 데이터 테이블
CREATE TABLE IF NOT EXISTS ohlcv (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(timestamp, symbol, exchange)
);

-- 실시간 거래 데이터 테이블
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    price REAL NOT NULL,
    amount REAL NOT NULL,
    side TEXT NOT NULL,  -- 'buy' 또는 'sell'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 차익거래 기회 테이블
CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    symbol TEXT NOT NULL,
    buy_exchange TEXT NOT NULL,
    sell_exchange TEXT NOT NULL,
    buy_price REAL NOT NULL,
    sell_price REAL NOT NULL,
    profit_percent REAL NOT NULL,
    total_fee_percent REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 온체인 트랜잭션 테이블
CREATE TABLE IF NOT EXISTS onchain_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    network TEXT NOT NULL,
    tx_hash TEXT NOT NULL,
    from_address TEXT NOT NULL,
    to_address TEXT,
    value REAL NOT NULL,
    gas_used INTEGER,
    block_number INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(network, tx_hash)
);

-- 각 테이블에 대한 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_ohlcv_timestamp ON ohlcv(timestamp);
CREATE INDEX IF NOT EXISTS idx_ohlcv_symbol ON ohlcv(symbol);
CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp);
CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS idx_arbitrage_timestamp ON arbitrage_opportunities(timestamp);
CREATE INDEX IF NOT EXISTS idx_onchain_tx_timestamp ON onchain_transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_onchain_tx_addresses ON onchain_transactions(from_address, to_address); 