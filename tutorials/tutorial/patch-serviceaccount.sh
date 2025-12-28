kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "docker-secret"}]}' --namespace tutorial
