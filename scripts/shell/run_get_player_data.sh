# Download the repo
curl -L -o repository.zip https://github.com/vaastav/Fantasy-Premier-League/archive/refs/heads/master.zip
# Unzip the downloaded file
unzip repository.zip

# Move the specific directory to the desired location
mv Fantasy-Premier-League-master/data data/vaastav-data

# Remove the extracted directory
rm -rf Fantasy-Premier-League-master

# Remove the ZIP file
rm repository.zip
