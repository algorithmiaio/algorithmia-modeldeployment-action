#!/bin/bash

# Install the dependencies of this repo to be able to run the notebook
pip3 install -r requirements.txt

# Clone the Algorithmia algorithm repository
CI_ALGO_DIR=$INPUT_ALGORITHMIA_ALGONAME"_CI"

if [ -z "$INPUT_ALGORITHMIA_PASSWORD" ]
then
    echo "Will clone algorithm repository hosted on Github"
    git clone https://"$INPUT_GITHUB_PAT"@"$INPUT_GIT_HOST"/"$INPUT_GITHUB_USERNAME"/"$INPUT_ALGORITHMIA_ALGONAME".git $CI_ALGO_DIR
else
    echo "Will clone algorithm repository hosted on Algorithmia"
    git clone https://"$INPUT_ALGORITHMIA_USERNAME":"$INPUT_ALGORITHMIA_PASSWORD"@"$INPUT_GIT_HOST"/git/"$INPUT_ALGORITHMIA_USERNAME"/"$INPUT_ALGORITHMIA_ALGONAME".git $CI_ALGO_DIR
fi

if [ -d $INPUT_ALGORITHMIA_ALGONAME ]
then
    echo "Will copy and push the contents of $INPUT_ALGORITHMIA_ALGONAME directory to Algorithm repository."
    cp -a "$INPUT_ALGORITHMIA_ALGONAME"/. $CI_ALGO_DIR/
else
    echo "Could not locate the algorithm directory to copy the contents."
fi

python3 /src/action_main.py

echo "Switching to the algorithm repo directory to push changes to the Algorithm repo."
cd $CI_ALGO_DIR
git config --global user.name "$INPUT_ALGORITHMIA_USERNAME"
git config --global user.email "$INPUT_ALGORITHMIA_EMAIL"
git status
git add .
git commit -m "Automated deployment via Github CI"
git push