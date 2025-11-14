terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "bus-system-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "bus-system-igw"
  }
}

# Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = element(["10.0.1.0/24", "10.0.2.0/24"], count.index)
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
  
  tags = {
    Name = "bus-system-public-${count.index + 1}"
  }
}

# RDS MySQL Database
resource "aws_db_instance" "mysql" {
  identifier             = "bus-system-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  db_name                = "bus_system"
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = "default.mysql8.0"
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
}

# Elasticache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "bus-system-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  port                 = 6379
  security_group_ids   = [aws_security_group.redis.id]
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "bus-system-cluster"
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "bus-system-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]
  subnets            = aws_subnet.public[*].id
}

# Auto Scaling Group
resource "aws_autoscaling_group" "api" {
  name                 = "bus-system-api"
  min_size             = 2
  max_size             = 10
  desired_capacity     = 2
  vpc_zone_identifier  = aws_subnet.public[*].id
  health_check_type    = "ELB"
  
  launch_template {
    id      = aws_launch_template.api.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "bus-system-api"
    propagate_at_launch = true
  }
}