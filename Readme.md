
# Table of Contents

1.  [UdaConnect](#org7406d9d)
    1.  [Overview](#org249a352)
        1.  [Classification of the project](#org7c01779)
        2.  [Project Background](#orge9b1fe8)
        3.  [Detailed Task](#org8ceec1c)
        4.  [Starter Code](#org890f197)
        5.  [Used Technologies](#org4e3f852)
    2.  [Starting the App](#org1f14360)
        1.  [Setup the environment](#org46afb50)
        2.  [Initialise K3s](#orgd49a1b4)
        3.  [Deploying the application](#orga9e87c2)
    3.  [Checking whether the app works in your environment](#org8a07a68)
        1.  [Verify Kubernetes Pods and services](#org33d20fd)
        2.  [Check service endpoints](#orgac416f1)
        3.  [Check gRPC and Kafka message stream to create new location data points](#orgeb398f2)



<a id="org7406d9d"></a>

# UdaConnect


<a id="org249a352"></a>

## Overview


<a id="org7c01779"></a>

### Classification of the project

This project is part of the Udacity Nanodegree &ldquo;[Cloud Native Application Architecture](https://www.udacity.com/course/cloud-native-application-architecture-nanodegree--nd064)&rdquo;. The task in this project is to &ldquo;refactor an application into a microservice architecture using message passing techniques that had been trained in the course&rdquo;.


<a id="orge9b1fe8"></a>

### Project Background

Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it&rsquo;s often hard to make these connections in the midst of all of these events&rsquo; excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.


<a id="org8ceec1c"></a>

### Detailed Task

You work for a company that is building an app that uses location data from mobile devices. Your company has built a Proof of concept (POC) application to ingest location data named UdaConnect. This POC was built with the core functionality of ingesting location and identifying individuals who have shared close geographic proximity.

Management loved the POC, so now that there is buy-in, we want to enhance this application. You have been tasked to enhance the POC application into a Minimum Viable Product (MVP) to handle the large volume of location data that will be ingested.

To do so, you will refactor this application into a microservice architecture using message passing techniques that you have learned in this course.


<a id="org890f197"></a>

### Starter Code

You can get started by forking, cloning, or downloading the [starter code](https://github.com/udacity/nd064-c2-message-passing-projects-starter).


<a id="org4e3f852"></a>

### Used Technologies

-   VirtualBox - Hypervisor allowing you to run multiple operating systems
-   Vagrant - Tool for managing virtual deployed environments
-   K3s - Lightweight distribution of K8s to easily develop against a local cluster
-   Flask - API webserver
-   SQLAlchemy - Database ORM
-   PostgreSQL - Relational database
-   PostGIS - Spatial plug-in for PostgreSQL enabling geographic queries
-   gRPC - A high performance, open source universal RPC framework
-   Kafka - Message streaming service


<a id="org1f14360"></a>

## Starting the App

The app is build in a way so that it can be installed and run in a Kubernetes Cluster.


<a id="org46afb50"></a>

### Setup the environment

-   Install Docker
-   Set up a DockerHub account
-   Set up kubectl
-   Install VirtualBox with at least version 6.0
-   Install Vagrant with at least version 2.0


<a id="orgd49a1b4"></a>

### Initialise K3s

To run the application, you will need a K8s cluster running locally and interface with it via kubectl. This project uses Vagrant with VirtualBox to run K3s.

In the project&rsquo;s root folder, run vagrant up.

    vagrant up

The command will take a while and will leverage VirtualBox to load an openSUSE OS and automatically install K3s.

After vagrant up is done, SSH into the Vagrant environment and retrieve the Kubernetes config file used by kubectl. Copy this file&rsquo;s contents into your local environment so that kubectl knows how to communicate with the K3s cluster.

When logged in to the vagrant box, run

    sudo cat /etc/rancher/k3s/k3s.yaml

Copy the output of that command into your clipboard and exit the SSH session. In your local environment create a file &ldquo;~/.kube/config&rdquo; and paste the content of the k3s.yaml file (your clipboard) into that file.

Test whether your environment works by running

    kubectl describe services

It should not return any errors.


<a id="orga9e87c2"></a>

### Deploying the application

The app has been refactored into several microservices that need to be deployed step by step.

1.  Setup Postgres database service

    Run the following commands to setup the postgres database service:
    
        kubectl apply -f modules/postgres/deployment/db-configmap.yaml
        kubectl apply -f modules/postgres/deployment/db-secret.yaml
        kubectl apply -f modules/postgres/deployment/geo-db.yaml
        
        # Seed the database with some initial test data.
        # 1. Get the pod name of the postgres database that you just created:
        kubectl get pods
        
        # 2. Than run
        sh modules/postgres/scripts/run_db_command.sh <POD_NAME>
    
    The above commands will deploy a postgres database on Kubernetes. The db is accessible under port 5432.

2.  Setup Person Service

    Run the following commands to setup the Person Service:
    
        kubectl apply -f modules/prsService/deployment/db-configmap.yaml
        kubectl apply -f modules/prsService/deployment/db-secret.yaml
        kubectl apply -f modules/prsService/deployment/prs-service-api.yaml
    
    Test the person service with URL / port: <http://localhost:30001/>

3.  Setup Location Service

    Run the following commands to setup the Location Service:
    
        kubectl apply -f modules/locService/deployment/db-configmap.yaml
        kubectl apply -f modules/locService/deployment/db-secret.yaml
        kubectl apply -f modules/locService/deployment/loc-service-api.yaml
    
    Test the location service with URL / port: <http://localhost:30002/>

4.  Setup Connection Service

    Run the following commands to setup the Connection Service:
    
        kubectl apply -f modules/conService/deployment/db-configmap.yaml
        kubectl apply -f modules/conService/deployment/db-secret.yaml
        kubectl apply -f modules/conService/deployment/con-service-api.yaml
    
    Test the connection service with URL / port: <http://localhost:30003/>

5.  Setup Frontend Service

    Run the following commands to setup the Connection Service:
    
        kubectl apply -f modules/frontend/deployment/udaconnect-app.yaml
    
    Test the Udaconnect frontend service with URL / port: <http://localhost:30000/>

6.  Setup Kafka message service

    [Apache Kafka packaged by Bitnami](https://bitnami.com/stack/kafka/helm) can be used to setup Kafka on the Kubernetes Cluster.
    
    1.  Install and configure Helm
    
        Run the following commands if you have not yet installed Helm with the bitnami repository.
        
        \#+begin<sub>src</sub> shell
        curl <https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get-helm-3> > get<sub>helm.sh</sub>
        chmod 700 get<sub>helm.sh</sub>
        ./get<sub>helm.sh</sub>
    
    2.  Deploy bitnami/kafka on the Kubernetes cluster
    
            helm repo add bitnami https://charts.bitnami.com/bitnami
            
            helm install loc-event-kafka bitnami/kafka
        
        The command should provide the following output:
        
        > Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:
        > 
        > loc-event-kafka.default.svc.cluster.local
        > 
        > Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:
        > 
        > loc-event-kafka-0.loc-event-kafka-headless.default.svc.cluster.local:9092
        > 
        > To create a pod that you can use as a Kafka client run the following commands:
        > 
        > kubectl run loc-event-kafka-client &#x2013;restart=&rsquo;Never&rsquo; &#x2013;image docker.io/bitnami/kafka:2.8.1-debian-10-r73 &#x2013;namespace default &#x2013;command &#x2013; sleep infinity
        > kubectl exec &#x2013;tty -i loc-event-kafka-client &#x2013;namespace default &#x2013; bash
        > 
        > PRODUCER:
        >     kafka-console-producer.sh \\
        > 
        > &#x2013;broker-list loc-event-kafka-0.loc-event-kafka-headless.default.svc.cluster.local:9092 \\
        > &#x2013;topic test
        > 
        > CONSUMER:
        >     kafka-console-consumer.sh \\
        > 
        > &#x2013;bootstrap-server loc-event-kafka.default.svc.cluster.local:9092 \\
        > &#x2013;topic test \\
        > &#x2013;from-beginning
    
    3.  Create a topic &ldquo;loc&rdquo;
    
        Login to the Kubernetes Cluster with:
        
            kubectl exec -it loc-event-kafka-0 /bin/bash
        
        Within the Kubernetes Cluster add the topic &ldquo;loc&rdquo; with:
        
            kafka-topics.sh --create --topic loc --bootstrap-server localhost:9092
    
    4.  Test the availability of the Kafka service
    
        Start a new terminal session and create a new pod that can be used as Kafka client:
        
            kubectl run loc-event-kafka-client --restart='Never' --image docker.io/bitnami/kafka:2.8.1-debian-10-r73 --namespace default --command -- sleep infinity
        
        After the pod is up and running, log in:
        
            kubectl exec --tty -i loc-event-kafka-client --namespace default -- bash
        
        Within the pod run a Kafka producer:
        
            kafka-console-producer.sh --broker-list loc-event-kafka-0.loc-event-kafka-headless.default.svc.cluster.local:9092 --topic loc
        
        That should give you a prompt in which you can enter some test messages.
        
        Now you need to check whether the messages are being passed over to the consumer. For that create an additional pod:
        
            kubectl run loc-event-kafka-client2 --restart='Never' --image docker.io/bitnami/kafka:2.8.1-debian-10-r73 --namespace default --command -- sleep infinity
        
        After the 2nd pod is up and running, log in:
        
            kubectl exec --tty -i loc-event-kafka-client2 --namespace default -- bash
        
        Within the pod run a Kafka consumer:
        
            kafka-console-consumer.sh --bootstrap-server loc-event-kafka.default.svc.cluster.local:9092 --topic loc --from-beginning
        
        That should give you a prompt in which you should see the test messages that you have entered before,

7.  Deploy the Location Event Producer

        kubectl apply -f modules/locEventProducer/deployment/kafka-configmap.yaml
        kubectl apply -f modules/locEventProducer/deployment/loc-event-api.yaml

8.  Deploy the Location Event Consumer

        kubectl apply -f modules/locEventConsumer/deployment/kafka-configmap.yaml
        kubectl apply -f modules/locEventConsumer/deployment/db-configmap.yaml
        kubectl apply -f modules/locEventConsumer/deployment/db-secret.yaml
        kubectl apply -f modules/locEventConsumer/deployment/loc-event-consumer-api.yaml


<a id="org8a07a68"></a>

## Checking whether the app works in your environment


<a id="org33d20fd"></a>

### Verify Kubernetes Pods and services

You should first check if the required Kubernetes pods and service are up and running. For this, please run:

    kubectl get pods
    
    kubectl get services

For each of the before mentioned deployments a pod and service should be up and running.


<a id="orgac416f1"></a>

### Check service endpoints

The following endpoints should work and not return any errors:

-   <http://localhost:30000>
-   <http://localhost:30001>
-   <http://localhost:30002>
-   <http://localhost:30003>


<a id="orgeb398f2"></a>

### Check gRPC and Kafka message stream to create new location data points

The pod &ldquo;loc-event-api-xxxxxxxx-xxxxx&rdquo; has been developed to let you test whether the gRPC - Kafka message stream works as expected.

1.  Log into the &ldquo;loc-event-api-xxxxxxxx-xxxxx&rdquo; pod with
    
        kubectl exec --tty -i loc-event-api-xxxxxxxx-xxxxx -- bash
2.  Within the pod run the python script &ldquo;pushTestEvents.py&rdquo;
    
        python pushTestEvents.py
3.  Check whether 5 new entries have been created in the location database.
    For that open <http://localhost:30002/api/locations> and verify that there are 5 new entries with a creation date of today.

