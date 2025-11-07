#!/bin/bash

set -e

echo "=== Configurando PetClinic Application ==="

# Fix DNS and update system
echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf

export DEBIAN_FRONTEND=noninteractive
echo "Atualizando sistema..."
for i in {1..3}; do
    apt-get update && break
    echo "Update retry $i failed, waiting..."
    sleep 30
done
apt-get upgrade -y --fix-missing

# Install Java 17 with retries
echo "Instalando Java 17..."
for i in {1..3}; do
    apt-get install -y openjdk-17-jdk curl wget netcat-openbsd --fix-missing && break
    echo "Java install retry $i failed, waiting..."
    sleep 30
    apt-get update
done

# Install Node.js 18 LTS with retries
echo "Instalando Node.js 18..."
for i in {1..3}; do
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && 
    apt-get install -y nodejs --fix-missing && break
    echo "Node.js install retry $i failed, waiting..."
    sleep 30
done

# Install Maven with retries
echo "Instalando Maven..."
for i in {1..3}; do
    apt-get install -y maven --fix-missing && break
    echo "Maven install retry $i failed, waiting..."
    sleep 30
    apt-get update
done

# Verificar versões
echo "Versões instaladas:"
java -version
node --version
npm --version
mvn --version

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> /home/vagrant/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin' >> /home/vagrant/.bashrc

# Aguardar PostgreSQL estar disponível (local)
echo "Aguardando PostgreSQL estar disponível..."
until nc -z localhost 5432; do
  echo "Aguardando PostgreSQL..."
  sleep 5
done
echo "PostgreSQL está disponível!"

# Change to application directory
cd /opt/petclinic

# Change ownership to vagrant user
chown -R vagrant:vagrant /opt/petclinic

# Make Maven wrapper executable and fix Windows line endings
chmod +x mvnw
# Fix potential Windows line endings in mvnw script
sed -i 's/\r$//' mvnw

# Build as vagrant user
echo "Compilando aplicação PetClinic (isso pode demorar alguns minutos)..."
sudo -u vagrant bash -c "
  export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
  export PATH=\$PATH:\$JAVA_HOME/bin
  cd /opt/petclinic
  
  # Clean and package (skip tests for faster build) - silent mode
  ./mvnw clean package -DskipTests -Dmaven.test.skip=true -q > /dev/null 2>&1
" 

# Verificar se o JAR foi criado
if [ ! -f target/*.jar ]; then
    echo "ERRO: JAR não foi criado."
    echo "Tentando compilar novamente com output visível para debug..."
    sudo -u vagrant bash -c "
      export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
      export PATH=\$PATH:\$JAVA_HOME/bin
      cd /opt/petclinic
      ./mvnw clean package -DskipTests -Dmaven.test.skip=true
    "
    exit 1
fi

echo "✅ Build concluído com sucesso!"

# Create systemd service for PetClinic
echo "Criando serviço systemd..."
cat > /etc/systemd/system/petclinic.service <<EOF
[Unit]
Description=Spring PetClinic Application
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=vagrant
Group=vagrant
WorkingDirectory=/opt/petclinic
Environment=JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
Environment=PATH=/usr/lib/jvm/java-17-openjdk-amd64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/petclinic
Environment=SPRING_DATASOURCE_USERNAME=petclinic
Environment=SPRING_DATASOURCE_PASSWORD=petclinic
ExecStart=/usr/lib/jvm/java-17-openjdk-amd64/bin/java -Xmx1g -jar target/hilla-petclinic-3.0.0-SNAPSHOT.jar --server.port=8080 --server.address=0.0.0.0
ExecStop=/bin/kill -15 \$MAINPID
Restart=always
RestartSec=15
StandardOutput=journal
StandardError=journal
SyslogIdentifier=petclinic

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl daemon-reload
systemctl enable petclinic

# Start service
echo "Iniciando serviço PetClinic..."
systemctl start petclinic > /dev/null 2>&1

# Wait a bit and check status
echo "Aguardando inicialização..."
sleep 10

# Check if service is running
if systemctl is-active --quiet petclinic; then
    echo "✅ PetClinic iniciado com sucesso!"
else
    echo "❌ Erro ao iniciar PetClinic. Verificando logs:"
    systemctl status petclinic --no-pager
fi

echo ""
echo "=== 🌸 PetClinic configurado com sucesso! ==="
echo "Aplicação disponível em:"
echo "  - 🌐 Externo: http://localhost:8080"
echo "  - 🔍 Interno: http://192.168.56.11:8080"