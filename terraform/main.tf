provider "aws" {
    region = "us-east-1"
}
resource "aws_instance" "chatbot_server" {
    ami = "ami-12345678"
    instance_type = "t2.micro"
    tags = {
    Name = "ChatbotServer"
    }
}
resource "aws_s3_bucket" "chatbot_logs" {
    bucket = "chatbot-logs-bucket"
}