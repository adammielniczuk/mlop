EC2_HOST="51.20.124.10"  
EC2_USER="ubuntu"  
KEY_FILE="kluczmlops.pem"  
IMAGE_NAME="model-serving:latest"

echo "Saving Docker image to tar"
docker save ${IMAGE_NAME} | gzip > model-serving.tar.gz


echo "Copying image" 
scp -i ${KEY_FILE} model-serving.tar.gz ${EC2_USER}@${EC2_HOST}:~

cat > /tmp/setup_docker.sh << 'EOF'
#!/bin/bash

if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."

    sudo apt-get update -y
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker ubuntu

fi

echo "Loading Docker image..."
sudo docker load < ~/model-serving.tar.gz

echo "Stopping old container..."
sudo docker stop model-server 2>/dev/null
sudo docker rm model-server 2>/dev/null


echo "Starting model server..."
sudo docker run -d \
  --name model-server \
  -p 3000:3000 \
  --restart unless-stopped \
  --memory="1g" \
  --cpus="1.0" \
  model-serving:latest

sleep 5


echo ""
echo "Container status:"
sudo docker ps | grep model-server


rm ~/model-serving.tar.gz
EOF

scp -i ${KEY_FILE} /tmp/setup_docker.sh ${EC2_USER}@${EC2_HOST}:~

echo "Running setup on EC2"
ssh -i ${KEY_FILE} ${EC2_USER}@${EC2_HOST} "chmod +x setup_docker.sh && ./setup_docker.sh"


rm model-serving.tar.gz
rm /tmp/setup_docker.sh

echo ""
echo "Deployment complete!"
echo ""
