#!/bin/bash

set -e

client_id=$ARM_CLIENT_ID
client_secret=$ARM_CLIENT_SECRET
tenant_id=$ARM_TENANT_ID
subscription_id=$ARM_SUBSCRIPTION_ID
registry=$ACR_REGISTRY
tags_to_keep=3


# Azure login
az_login () {
    echo "Logging into Azure..."
    az login \
    --service-principal \
    -u $client_id \
    -p $client_secret \
    --tenant $tenant_id

    az account set \
    --subscription $subscription_id
}

# Retrieve robot-shop/* Repositories 
get_repositories () {
    echo "Retrieving robot-shop/* repositories under $registry"
    az acr repository list \
    -n "$registry" \
    | jq -r '.[] | select(.|test("^robot-shop."))' \
    > "$registry"_repositories.txt
}

# Delete digests
delete_digests () {
    digests_file="$1"
    repository="robot-shop/"$(echo $digests_file | awk -F '_' '{print $2}')

    echo "Deleting Digests from $digests_file"
    while read -r digest; do
        az acr repository delete \
        -n "$registry" \
        --image "$repository@$digest" \
        --yes 
    done \
    < $digests_file
}

# Retrieve oldest digests
get_digests_to_remove () {
    repository="$1"
    repository_name=$(echo $repository | awk -F '/' '{print $2}')

    > "$registry"_"$repository_name"_digests_develop_tag.txt
    > "$registry"_"$repository_name"_digests_to_remove.txt

    # Retrieve develop-* tags
    echo "Retrieving develop-* tags for $repository"
    az acr repository show-tags \
    -n "$registry"\
    --repository "$repository"\
    --detail \
    --orderby time_desc \
    | jq -r '.[] | select(.name|test("^develop."))' | jq -r '.digest' \
    >> "$registry"_"$repository_name"_digests_develop_tag.txt

    tag_count=$(wc -l < "$registry"_"$repository_name"_digests_develop_tag.txt)

    if [[ $tag_count -gt $tags_to_keep ]]; then
        tail -n $(( $tag_count-$tags_to_keep )) "$registry"_"$repository_name"_digests_develop_tag.txt \
        >> "$registry"_"$repository_name"_digests_to_remove.txt
    fi

    # Retrieve all other tags
    echo "Retrieving all other tags for $repository"
    az acr repository show-tags \
    -n "$registry" \
    --repository "$repository" \
    --detail \
    | jq -r '.[] | select(.name|test("^develop.") | not) ' | jq -r '.digest' \
    >> "$registry"_"$repository_name"_digests_to_remove.txt

    rm "$registry"_"$repository_name"_digests_develop_tag.txt
}

mkdir "$registry"_digests
cd "$registry"_digests

az_login
get_repositories

mkdir digests_to_remove
cd digests_to_remove

while read -r repository; do
    get_digests_to_remove $repository
done \
< ../"$registry"_repositories.txt

for file in *; do
    delete_digests $file
done

rm -rf "$registry"_digests