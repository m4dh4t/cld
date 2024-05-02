# Task 3 - Add and exercise resilience

By now you should have understood the general principle of configuring, running and accessing applications in Kubernetes. However, the above application has no support for resilience. If a container (resp. Pod) dies, it stops working. Next, we add some resilience to the application.

## Subtask 3.1 - Add Deployments

In this task you will create Deployments that will spawn Replica Sets as health-management components.

Converting a Pod to be managed by a Deployment is quite simple.

  * Have a look at an example of a Deployment described here: <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>

  * Create Deployment versions of your application configurations (e.g. `redis-deploy.yaml` instead of `redis-pod.yaml`) and modify/extend them to contain the required Deployment parameters.

  * Again, be careful with the YAML indentation!

  * Make sure to have always 2 instances of the API and Frontend running.

  * Use only 1 instance for the Redis-Server. Why?

    > Because the Redis-Server is a stateful service and thus cannot be scaled horizontally. If we were to run multiple instances of the Redis-Server, we would need to implement a mechanism to synchronize the data between the instances, as each instance would have its own data. This would make the system more complex and harder to maintain. By running only one instance of the Redis-Server, we ensure that the data is consistent and that the system is easier to manage.

  * Delete all application Pods (using `kubectl delete pod ...`) and replace them with deployment versions.

  * Verify that the application is still working and the Replica Sets are in place. (`kubectl get all`, `kubectl get pods`, `kubectl describe ...`)

## Subtask 3.2 - Verify the functionality of the Replica Sets

In this subtask you will intentionally kill (delete) Pods and verify that the application keeps working and the Replica Set is doing its task.

Hint: You can monitor the status of a resource by adding the `--watch` option to the `get` command. To watch a single resource:

```sh
$ kubectl get <resource-name> --watch
```

To watch all resources of a certain type, for example all Pods:

```sh
$ kubectl get pods --watch
```

You may also use `kubectl get all` repeatedly to see a list of all resources.  You should also verify if the application stays available by continuously reloading your browser window.

  * What happens if you delete a Frontend or API Pod? How long does it take for the system to react?

    > After deleting a Frontend or API Pod, the system will automatically create a new Pod to replace the deleted one. This process takes a few seconds. During this time, the application is available, as the other replica is still running. The new Pod will be added to the Replica Set and the application will continue to work as expected.

  * What happens when you delete the Redis Pod?

    > When the Redis Pod is deleted, the system will automatically create a new Pod to replace the deleted one. However, the new Pod will not be able to recover the data from the previous Pod, as the data is stored in the persistent volume. The new Pod will start with an empty database, but there seems to be an impact on the application behavior, as new TODOs cannot be created. When issuing a new request, the application will throw an exception in the browser console: `todos.js:13 Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'id')`. We can find the cause by looking at the network tab in the browser developer tools, where we can see that the POST request to the API endpoint `/api/todos` returns a `200 OK` status although the response is empty. When looking at the API logs, we can also see that the response time went from ~4ms to ~1ms, which is abnormally fast. This may indicate that the API was not able to connect to the Redis server and thus ended the request prematurely. To fix this issue, we need to restart the API deployment, which will create fresh Pods that are able to process the requests correctly again.

  * How can you change the number of instances temporarily to 3? Hint: look for scaling in the deployment documentation

    > To change the number of instances temporarily to 3, we can use the following command: `kubectl scale deployment <deployment-name> --replicas=3`. This will scale the deployment to 3 replicas. To scale it back to 2 replicas, we can use the same command with `--replicas=2`.

  * What autoscaling features are available? Which metrics are used?

    > The autoscaling features available are Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA). The Horizontal Pod Autoscaler automatically scales the number of Pods in a replication controller, deployment, replica set, or stateful set based on observed CPU utilization (or, with custom metrics support, on some other application-provided metrics). The Vertical Pod Autoscaler automatically adjusts the CPU and memory resource requests for the pods according to their load. Other options include Cluster Autoscaler, which automatically adjusts the size of a Kubernetes cluster so that all pods have a place to run and are not starved for resources, Event-driven Autoscaling, which allows you to scale your application based on events, and Custom Metrics API, which allows you to scale your application based on custom metrics, and Scheduled Autoscaling, which allows you to scale your application based on a schedule, for example in order to reduce resource consumption during off-peak hours.

  * How can you update a component? (see "Updating a Deployment" in the deployment documentation)

    > To update a component, we can use the `kubectl set image` command. For example, to update the image of the frontend deployment, we can use the following command: `kubectl set image deployment/frontend-deploy frontend=frontend:v2`. This will update the image of the frontend deployment to `frontend:v2`. Alternatively, we can edit the deployment configuration file and apply the changes using `kubectl apply -f <file>`, or we can use the `kubectl edit` command to edit the deployment configuration on the fly.

## Subtask 3.3 - Put autoscaling in place and load-test it

On the GKE cluster deploy autoscaling on the Frontend with a target CPU utilization of 30% and number of replicas between 1 and 4.

Load-test using Vegeta (500 requests should be enough).

> [!NOTE]
>
> - The autoscale may take a while to trigger.
>
> - If your autoscaling fails to get the cpu utilization metrics, run the following command
>
>   - ```sh
>     $ kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
>     ```
>
>   - Then add the *resources* part in the *container part* in your `frontend-deploy` :
>
>   - ```yaml
>     spec:
>       containers:
>         - ...:
>           env:
>             - ...:
>           resources:
>             requests:
>               cpu: 10m
>     ```
>

## Deliverables

Document your observations in the lab report. Document any difficulties you faced and how you overcame them. Copy the object descriptions into the lab report.

> When running running Vegeta, we saw a steep spike in CPU usage in the frontend deployment dashboard of the GKE cluster. As the message `Unable to read all metrics` was shown next to the Horizontal Pod Autoscaler status in the dashboard, we added `metrics-server` to the cluster and added the `resources` part to the `frontend-deploy.yaml` file to periodically collect CPU usage metrics. After this, the Horizontal Pod Autoscaler was able to successfully calculate a replica count from the CPU resource utilization and scaled the frontend deployment to 4 replicas, while the application was still available. Once the CPU usage dropped below the target of 30%, the Horizontal Pod Autoscaler scaled the frontend deployment back to 1 replica (our minimum number of replicas).

```````sh
❯ kubectl describe deployment
Name:                   api-deployment
Namespace:              default
CreationTimestamp:      Thu, 02 May 2024 14:32:58 +0200
Labels:                 app=todo
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               component=api
Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=todo
           component=api
  Containers:
   api:
    Image:      icclabcna/ccp2-k8s-todo-api
    Port:       8081/TCP
    Host Port:  0/TCP
    Environment:
      REDIS_ENDPOINT:  redis-svc
      REDIS_PWD:       ccp2
    Mounts:            <none>
  Volumes:             <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   api-deployment-664fbdf7d9 (2/2 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  3m13s  deployment-controller  Scaled up replica set api-deployment-664fbdf7d9 to 2


Name:                   frontend-deployment
Namespace:              default
CreationTimestamp:      Thu, 02 May 2024 14:31:29 +0200
Labels:                 app=todo
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               component=frontend
Replicas:               4 desired | 4 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=todo
           component=frontend
  Containers:
   frontend:
    Image:      icclabcna/ccp2-k8s-todo-frontend
    Port:       8080/TCP
    Host Port:  0/TCP
    Requests:
      cpu:  10m
    Environment:
      API_ENDPOINT_URL:  http://api-svc:8081
    Mounts:              <none>
  Volumes:               <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   frontend-deployment-859d5f8544 (4/4 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  4m41s  deployment-controller  Scaled up replica set frontend-deployment-859d5f8544 to 2
  Normal  ScalingReplicaSet  2m20s  deployment-controller  Scaled up replica set frontend-deployment-859d5f8544 to 4 from 2


Name:                   redis-deployment
Namespace:              default
CreationTimestamp:      Thu, 02 May 2024 14:33:02 +0200
Labels:                 app=todo
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               component=redis
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=todo
           component=redis
  Containers:
   redis:
    Image:      redis
    Port:       6379/TCP
    Host Port:  0/TCP
    Args:
      redis-server
      --requirepass ccp2
      --appendonly yes
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   redis-deployment-56fb88dd96 (1/1 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  3m9s  deployment-controller  Scaled up replica set redis-deployment-56fb88dd96 to 1

❯ kubectl describe horizontalpodautoscaler.autoscaling
Name:                                                  frontend-deployment
Namespace:                                             default
Labels:                                                <none>
Annotations:                                           <none>
CreationTimestamp:                                     Thu, 02 May 2024 14:33:21 +0200
Reference:                                             Deployment/frontend-deployment
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  0% (0) / 30%
Min replicas:                                          1
Max replicas:                                          4
Deployment pods:                                       4 current / 4 desired
Conditions:
  Type            Status  Reason               Message
  ----            ------  ------               -------
  AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one, applying the highest recent recommendation
  ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooManyReplicas      the desired replica count is more than the maximum replica count
Events:
  Type    Reason             Age    From                       Message
  ----    ------             ----   ----                       -------
  Normal  SuccessfulRescale  4m29s  horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
```````

```yaml
# redis-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  labels:
    app: todo
spec:
  replicas: 1
  selector:
    matchLabels:
      component: redis
  template:
    metadata:
      labels:
        component: redis
        app: todo
    spec:
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379
        args:
        - redis-server
        - --requirepass ccp2
        - --appendonly yes
```

```yaml
# api-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  labels:
    app: todo
spec:
  replicas: 2
  selector:
    matchLabels:
      component: api
  template:
    metadata:
      labels:
        component: api
        app: todo
    spec:
      containers:
      - name: api
        image: icclabcna/ccp2-k8s-todo-api
        ports:
        - containerPort: 8081
        env:
        - name: REDIS_ENDPOINT
          value: redis-svc
        - name: REDIS_PWD
          value: ccp2
```

```yaml
# frontend-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  labels:
    app: todo
spec:
  replicas: 2
  selector:
    matchLabels:
      component: frontend
  template:
    metadata:
      labels:
        component: frontend
        app: todo
    spec:
      containers:
      - name: frontend
        image: icclabcna/ccp2-k8s-todo-frontend
        ports:
        - containerPort: 8080
        env:
        - name: API_ENDPOINT_URL
          value: http://api-svc:8081
        resources:
          requests:
            cpu: 10m
```
