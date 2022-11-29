# Ubuntu 22.04 Init env
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
sudo apt update
sudo apt upgrade
sudo apt install build-essential zip unzip

# Install python
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
shasum -a 256 Miniconda3-latest-Linux-x86_64.sh | grep 78f39f9bae971ec1ae7969f0516017f2413f17796670f7040725dd83fcff5689
bash Miniconda3-latest-Linux-x86_64.sh

# Install Java
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 8.0.352-amzn
sdk install java 11.0.17-amzn
export JAVA8_HOME="$HOME/.sdkman/candidates/java/8.0.352-amzn"
export JAVA11_HOME="$HOME/.sdkman/candidates/java/11.0.17-amzn"

# Install esrally and opensearch-benchmark
pip install esrally==2.3.0
pip install opensearch-benchmark

# System config
# https://www.elastic.co/guide/en/elasticsearch/reference/master/setting-system-settings.html
sudo sysctl -w vm.max_map_count=262144
