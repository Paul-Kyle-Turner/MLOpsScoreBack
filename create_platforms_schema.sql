
--drop schema platforms cascade;

create schema if not exists platforms;

create type platforms.platform_types as enum (
	'hyperscaler',
	'gpu_cloud',
	'edge_cloud',
	'hybrid_cloud',
	'private_cloud',
	'specialized_ai',
	'container_platform',
	'serverless',
	'other'
);

create type platforms.datacenter_tier as enum (
	'tier_1',
	'tier_2',
	'tier_3',
	'tier_4',
	'tier_5',
	'colocation', 
	'edge',
	'hybrid',
	'unknown'
);

create type platforms.pricing_type as enum (
	'on_demand',
	'reserved',
	'spot',
	'preemptible',
	'dedicated',
	'burstable'
);

create type platforms.compliance_status as enum (
	'certified',
	'in_progress',
	'planned',
	'not_applicable',
	'unknown'
);

create type platforms.billing_increment as enum (
	'per_second',
	'per_minute',
	'per_hour',
	'per_day',
	'per_month',
	'per_year',
	'one_time',
	'custom'
);

create table if not exists platforms.network_capabilities (
	id bigint generated by default as identity primary key,
	bandwidth_gbps decimal(4),
	network_type varchar(1024),
	interconnect_technology varchar(1024),
	vpc_support bool,
	load_balancing bool,
	cdn_integration bool,
	private_networking bool
);

create table if not exists platforms.security_features (
	id bigint generated always as identity primary key,
	encryption_at_rest bool,
	encryption_in_transit bool,
	key_management bool,
	identity_management bool,
	network_security bool,
	vulnerability_scanning bool,
	security_monitoring bool,
	penetration_testing bool
);

create table if not exists platforms.platform_information (
	id bigint generated always as identity primary key,
	platform_name varchar(512) not null,
	platform_type platforms.platform_types,
	parent_company varchar(512),
	founded_date timestamp with time zone,
	headquarters varchar(512),
	website_url varchar(1024),
	documentation_url varchar(1024),
	primary_datacenter_tier platforms.datacenter_tier,
	total_datacenters int,
	edge_locations int,
	custom_configuration_support bool,
	bare_metal_available bool,
	networking_id bigint 
		references platforms.network_capabilities(id)
		on delete cascade,
	security_id bigint 
		references platforms.security_features(id)
		on delete cascade,
	sla_uptime decimal(20),
	specializations varchar(1024)[],
	target_markets varchar(1024)[],
	notable_customers varchar(1024)[],
	partnerships varchar(512)[],
	last_updated timestamp with time zone default current_timestamp,
	data_sources varchar(1024)[]
);

create table if not exists platforms.geographic_regions (
	id bigint generated by default as identity primary key,
	platform_id bigint not null
		references platforms.platform_information(id),
	region_name varchar(256) not null,
	region_code varchar(256) not null,
	country char(2) not null,
	availability_zones int,
	datacenter_tier platforms.datacenter_tier,
	edge_location bool
);

create table if not exists platforms.compliance_certification (
	id bigint generated by default as identity primary key,
	platform_id bigint not null
		references platforms.platform_information(id),
	certification_name varchar(100) not null,
	certification_date timestamp with time zone,
	certifying_body varchar(256),
	certificate_url varchar(512)
);

create table if not exists platforms.pricing_model (
	id bigint generated by default as identity primary key,
	compute_instance_id bigint not null
		references platforms.platform_information(id),
	pricing_type platforms.pricing_type,
	price_per_hour decimal(6),
	price_per_month decimal(6),
	minimum_commitment varchar(1024),
	billing_increment platforms.billing_increment
);


create table if not exists platforms.compute_instance (
	id bigint generated by default as identity primary key,
	platform_id bigint not null
		references platforms.platform_information(id),
	instance_name varchar(512),
	instance_family varchar(512),
	vcpus int not null,
	memory_gb numeric(2),
	storage_gb numeric(2),
	storage_type varchar(128),
	gpu_count int,
	gpu_type varchar(512),
	gpu_memory_gb numeric(2),
	network_performance varchar(512),	
	architecture varchar(128),
	specialized_hardware varchar(1024)
);




create table if not exists platforms.support_tier (
	id bigint generated by default as identity primary key,
	platform_id bigint not null
		references platforms.platform_information(id),
	tier_name varchar(256),
	average_response_time varchar(512),
	channels varchar(256)[],
	hours varchar(512),
	price varchar(512),
	premium_features varchar(1024)[]
);

create table if not exists platforms.proprietary_software(
	id bigint generated by default as identity primary key,
	platform_id bigint not null
		references platforms.platform_information(id),
	software_name varchar(512),
	software_type varchar(256),
	description varchar(1024),
	version varchar(128),
	open_source bool,
	license_type varchar(128),
	documentation_url varchar(1024),
	github_url varchar(1024),
	use_cases varchar(1024)[]
);

create table if not exists platforms.proprietary_hardware(
	id bigint generated by default as identity primary key,
	platform_id bigint not null
		references platforms.platform_information(id),
	hardware_name varchar(512),
	hardware_type varchar(256),
	description varchar(1024),
	specifications jsonb,
	performance_metrics jsonb,
	availability varchar(512),
	generation varchar(128),
	manufacturing_partner varchar(512)[],
	use_cases varchar(1024)[]
);


