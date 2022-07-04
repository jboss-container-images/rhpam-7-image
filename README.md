# Business Automation Manager Open Editions 7 standalone CeKit Module

This repo contains the base module that installs the product artifacts in the target OpenShift image.

does not need to be built manually, it is used as a cekit module  that will builds the base image that contains
the EAP with the application layer (business central, kieserver, etc.) on it without any kind of configuration, we call
it standalone-image, all the configuration will be made by the *-openshift repositories which contains the image
descriptors with all modules that will be installed. In this repo you will find the basics like which artifact
(kieserver, business central, etc) is being used to build the openshift images.
Let’s inspect the rhpam-7-businesscentral cekit module:


```yaml
schema_version: 1
name: "rhpam-7-businesscentral"
version: "1.0"
description: "IBM Business Central 8.0 installer"
labels:
- name: "org.jboss.product"
  value: "ibm-bamoe-businesscentral"
- name: "org.jboss.product.version"
  value: "8.0.0"
- name: "org.jboss.product.rhpam-businesscentral.version"
  value: "8.0.0"
envs:
- name: "JBOSS_PRODUCT"
  value: "ibm-bamoe-businesscentral"
- name: "RHPAM_BUSINESS_CENTRAL_VERSION"
  value: "8.0.0"
- name: "PRODUCT_VERSION"
  value: "8.0.0"
- name: "BUSINESS_CENTRAL_DISTRIBUTION_ZIP"
  value: "rhpam_business_central_distribution.zip"
- name: "BUSINESS_CENTRAL_DISTRIBUTION_EAP"
  value: "jboss-eap-7.2"
ports:
- value: 8001
artifacts:
- name: "rhpam_business_central_distribution.zip"
  # rhpam-8.0.0.redhat-211006-business-central-eap7-deployable.zip
  md5: "4194d7aa9613a52a1c5045e0236f94d5"
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
 - **branch-overrides.yaml**: overrides file which uses the latest stable version for external dependencies.
 - **tag-overrides.yaml**: Used to override the branchs to use the final tags to rebuild released images, for CVE respins.
 - **image.yaml**: the main image descriptor file, here are all the pieces and configuration needed to build an image. (Deprecated)


### Update versions

Before each release, there is a need to update the product version on each repository that composes the Container
Images.
In this repo you will find the **scripts** directory which containers the `update-version.py` script which helps to
update the version to the next release interation smoothly.

This script requires python 3.


See its usage:
```bash
$ python scripts/update-version.py --help
usage: update-version.py [-h] [-v T_VERSION] [--confirm]

RHDM Version Manager

optional arguments:
  -h, --help    show this help message and exit
  -v T_VERSION  update everything to the next version
  --confirm     if not set, script will not update the rhdm modules. (Dry run)
```


There is two options to run it, a dry-run option which will only print for you the changes, useful if you want just to see
how the changes will looks like after the script is executed, and if the chages are correct, the `--confirm` flag
should be used.

 ##### Found a issue?
 Please submit a issue [here](https://issues.jboss.org/projects/KIECLOUD) or send us a email: bsig-cloud@redhat.com.
