CREATE DATABASE hml;

use hml;

DROP TABLE user;;/*SkipError*/
CREATE TABLE user(
    id VARCHAR(36) NOT NULL   COMMENT 'ID' ,
    email VARCHAR(128) NOT NULL   COMMENT '邮箱' ,
    username VARCHAR(128) NOT NULL   COMMENT '用户名' ,
    type VARCHAR(36)    COMMENT '角色' ,
    password VARCHAR(36) NOT NULL   COMMENT '密码' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间 用户创建时间' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间 用户信息更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '用户表 ';;

ALTER TABLE user COMMENT '用户表';;
DROP TABLE device;;/*SkipError*/
CREATE TABLE device(
    id VARCHAR(36) NOT NULL   COMMENT '设备id' ,
    created_by VARCHAR(36) NOT NULL   COMMENT '创建人' ,
    name VARCHAR(128)    COMMENT '自定义设备名' ,
    token TEXT NOT NULL   COMMENT 'token' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间' ,
    info TEXT    COMMENT '设备信息' ,
    PRIMARY KEY (id)
) COMMENT = '设备表 ';;

ALTER TABLE device COMMENT '设备表';;
DROP TABLE model;;/*SkipError*/
CREATE TABLE model(
    id VARCHAR(36) NOT NULL   COMMENT '模型id' ,
    created_by VARCHAR(36) NOT NULL   COMMENT '拥有者id' ,
    name TEXT    COMMENT '模型名' ,
    type VARCHAR(36)    COMMENT '数据集类型' ,
    code_path TEXT    COMMENT '模型路径' ,
    config TEXT    COMMENT '配置' ,
    public INT    COMMENT '公开' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '模型表 ';;

ALTER TABLE model COMMENT '模型表';;
DROP TABLE dataset;;/*SkipError*/
CREATE TABLE dataset(
    id VARCHAR(36) NOT NULL   COMMENT '数据集id' ,
    dataturks_id VARCHAR(36)    COMMENT 'dataturks的对应id' ,
    name TEXT    COMMENT '数据集名' ,
    created_by VARCHAR(36) NOT NULL   COMMENT '创建者id' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间' ,
    public INT    COMMENT '访问权限' ,
    config TEXT    COMMENT '配置文件' ,
    PRIMARY KEY (id)
) COMMENT = '数据表 ';;

ALTER TABLE dataset COMMENT '数据表';;
DROP TABLE task;;/*SkipError*/
CREATE TABLE task(
    id VARCHAR(36) NOT NULL   COMMENT '任务id' ,
    name VARCHAR(36)    COMMENT '任务名' ,
    created_by VARCHAR(36)    COMMENT '创建人' ,
    created_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间' ,
    type VARCHAR(36)    COMMENT '任务类型' ,
    public INT    COMMENT '是否为公开任务' ,
    dataset_id VARCHAR(36)    COMMENT '数据集id' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '任务表 ';;

ALTER TABLE task COMMENT '任务表';;
DROP TABLE train;;/*SkipError*/
CREATE TABLE train(
    id VARCHAR(36) NOT NULL   COMMENT '训练状态id' ,
    task_id VARCHAR(36) NOT NULL   COMMENT '任务id' ,
    model_id VARCHAR(36)    COMMENT '模型id' ,
    created_by VARCHAR(36)    COMMENT '创建人' ,
    device_id VARCHAR(36)    COMMENT '设备id' ,
    status INT    COMMENT '状态' ,
    detail TEXT    COMMENT '训练细节' ,
    updated_time DATETIME   DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间' ,
    PRIMARY KEY (id)
) COMMENT = '训练状态表 ';;

ALTER TABLE train COMMENT '训练状态表';;
