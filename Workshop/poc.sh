aws lambda invoke \
    --function-name cld-workshopteam9 \
    --cli-binary-format raw-in-base64-out \
    --payload '{ "places": ["HEIG-VD, Yverdon-les-Bains", "EPFL, Ecublens"] }' \
    response.json
