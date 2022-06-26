terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_vpc" "photographic_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "photographic-vpc"
  }
}

resource "aws_internet_gateway" "photographic_igw" {
  vpc_id = aws_vpc.photographic_vpc.id

  tags = {
    Name = "photographic-igw"
  }
}

resource "aws_route_table" "photographic_rtb_public" {
  vpc_id = aws_vpc.photographic_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.photographic_igw.id
  }

  tags = {
    Name = "photographic-rtb-public"
  }
}

resource "aws_route_table" "photographic_rtb_private" {
  vpc_id = aws_vpc.photographic_vpc.id

  route = []

  tags = {
    Name = "photographic-rtb-private"
  }
}

resource "aws_subnet" "photographic_subnet_public_a" {
  vpc_id            = aws_vpc.photographic_vpc.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "eu-north-1a"

  tags = {
    Name = "photographic-subnet-public-eu-north-1a"
  }
}

resource "aws_subnet" "photographic_subnet_public_b" {
  vpc_id            = aws_vpc.photographic_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-north-1b"

  tags = {
    Name = "photographic-subnet-public-eu-north-1b"
  }
}

resource "aws_subnet" "photographic_subnet_private_a" {
  vpc_id            = aws_vpc.photographic_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-north-1a"

  tags = {
    Name = "photographic-subnet-private-eu-north-1a"
  }
}

resource "aws_subnet" "photographic_subnet_private_b" {
  vpc_id            = aws_vpc.photographic_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "eu-north-1b"

  tags = {
    Name = "photographic-subnet-private-eu-north-1b"
  }
}

resource "aws_db_subnet_group" "photographic_db_subnet_group" {
  name       = "photographic-db-subnet-group"
  subnet_ids = [
    aws_subnet.photographic_subnet_private_a.id,
    aws_subnet.photographic_subnet_private_b.id
  ]
}

resource "aws_security_group" "web" {
  name        = "web"
  description = "Allow public access over HTTP/HTTPS and management from defined IPs"
  vpc_id      = aws_vpc.photographic_vpc.id

  ingress {
    description = "Public HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Public HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Public HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from approved networks"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["185.127.100.0/24", "46.212.130.203/32"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_security_group" "database" {
  name        = "database"
  description = "Allow access from web security group"
  vpc_id      = aws_vpc.photographic_vpc.id

  ingress {
    description     = "PostgreSQL from web security group"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
}
