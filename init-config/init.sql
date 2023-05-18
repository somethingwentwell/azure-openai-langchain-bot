CREATE DATABASE chat_history;

\c chat_history; 

CREATE TABLE agent_log (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(255) NOT NULL,
  callback_type VARCHAR(255) NOT NULL,
  log JSON NOT NULL
);