# Red Hat Process Automation Manager 7 standalone CeKit Module

This repo contains the base module that installs the product artifacts in the target OpenShift image.

does not need to be built manually, it is used as a cekit module  that will builds the base image that contains
the EAP with the application layer (business central, kieserver, etc.) on it without any kind of configuration, we call
it standalone-image, all the configuration will be made by the *-openshift repositories which contains the image
descriptors with all modules that will be installed. In this repo you will find the basics like which artifact
(kieserver, business central, etc) is being used to build the openshift images.
Let’s inspect the rhpam-7-businesscentral cekit module:


```yaml
---
schema_version: 1
name: "rhpam-7-businesscentral"
version: "1.0"
description: "Red Hat Business Central 7.5 install"
labels:
- name: "org.jboss.product"
  value: "rhpam-businesscentral"
- name: "org.jboss.product.version"
  value: "7.5.1"
- name: "org.jboss.product.rhpam-businesscentral.version"
  value: "7.5.1"
envs:
- name: "JBOSS_PRODUCT"
  value: "rhpam-businesscentral"
- name: "RHPAM_BUSINESS_CENTRAL_VERSION"
  value: "7.5.1"
- name: "PRODUCT_VERSION"
  value: "7.5.1"
- name: "BUSINESS_CENTRAL_DISTRIBUTION_ZIP"
  value: "business_central_distribution.zip"
- name: "BUSINESS_CENTRAL_DISTRIBUTION_EAP"
  value: "jboss-eap-7.2"
ports:
- value: 8001
artifacts:
- name: "BUSINESS_CENTRAL_DISTRIBUTION_ZIP"
  target: "business_central_distribution.zip"
  # rhpam-7.5.1-business-central-eap7-deployable.zip
  md5: "4de4389d25ae9d32cd7cc5fac7500d1f"
run:
  user: 185
  cmd:
  - "/opt/eap/bin/standalone.sh"
  - "-b"
  - "0.0.0.0"
  - "-c"
  - "standalone.xml"
execute:
- script: "install"
```

In the file above we set the most important configurations to which defines:
    - the product
    - the product version
    - the product zip artifact, which will be deployed on the final OpenShift image.

Note the *BUSINESS_CENTRAL_DISTRIBUTION.ZIP* env, its value will be the artifact name that, when the build is completed,
is placed in the `/<images_source_dir>/rhpam-7-openshift-image/businesscentral/target/image` directory,
note that it is on the rpam-7-openshift-image repository. The **module.yaml** file above is a example of
the base module used to configure the product bits into the final OpenShift image. All OpenShift images have a
similar module descriptor, and these modules (the base modules) are one of the first module listed in the
 *-openshift image’s image.yaml file.



This repo is used to build the final OpenShift images, they contain a set of yaml files, below you will find each
file and its purpose, all the modules have the same files, as described below:

 - **container.yaml**: used by OSBS builds.
 - **content_sets.yaml**: define the yum repositories needed to install dependencies for the image.
 - **branch-overrides.yaml**: overrides file which uses the latest stable version for external dependencies. The module.yaml and image.yaml always refer to master branch.
 - **tag-overrides.yaml**: Used to override the branchs to use the final tags to rebuild released images, for CVE respins.
 - **image.yaml**: the main image descriptor file, here are all the pieces and configuration needed to build an image. (Deprecated)


 ##### Found a issue?
 Please submit a issue [here](https://issues.jboss.org/projects/KIECLOUD) or send us a email: bsig-cloud@redhat.com.
