CREATE DATABASE server_monitoring;

USE server_monitoring;

CREATE TABLE server_metrics (
id INT IDENTITY(1,1) PRIMARY KEY,
timestamp DATETIME,
server_id VARCHAR(50),
cpu_usage FLOAT,
memory_usage FLOAT,
disk_usage FLOAT,
network_usage FLOAT,
location VARCHAR(50),
os_type VARCHAR(50),
instance_size VARCHAR(50),
cpu_status VARCHAR(20),
memory_status VARCHAR(20),
alert VARCHAR(50)
);