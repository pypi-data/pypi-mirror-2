ec2selector is a tool to select an EC2 AMI (Amazon Machine Image) from those 
available on Amazon.
There are three basic ways in which you can use this tool.

# Selecting an image knowing its ID

If you already know the image ID, you can use ec2selector to make sure that 
such an instance is still available on Amazon for a given region, e.g.:

    from ec2selector import EC2Selector
    EC2Selector().select(region_id='us-east-1', image_id='ami-ed16f984')

will return `Image:ami-ed16f984` if such an image exists on US East 1.

# Selecting an image specifying a set of properties

If you don't know the image ID, you can specify a set of properties to match 
one of the images available on Amazon. The properties you can filter on are:

* name
* owner_id
* virtualization_type
* image_type
* architecture

You can also use the properties followed by '_contains' to specify a partial 
match. For instance, the following commands will return an AMI in US East,
owned by the user 'alestic' with a 'machine' image at 64bit, and whose name 
includes the string 'ubuntu-10':

    from ec2selector import EC2Selector
    EC2Selector().select(region_id='us-east-1', filters={
        'name_contains': 'ubuntu-10', 
        'owner_id':'063491364108',     # corresponds to 'alestic'
        'image_type': 'machine', 
        'virtualization_type':'paravirtual',
        'architecture': 'x86_64', 
    })

# Selecting an image with an interactive prompt

Finally, if you do not specify enough filters to get exactly *one* image,
you will get an interactive shell to add more filters or pick one of the
available images. For instance, this is a prompt session:

    >>> from ec2selector import EC2Selector
    >>> EC2Selector().select()
    
    5 regions available
    Please pick one of the available options:
     [0] eu-west-1
     [1] us-east-1
     [2] ap-northeast-1
     [3] us-west-1
     [4] ap-southeast-1
    
    > 0
    Loading list of available EC2 images for eu-west-1 with filters: None, might take a while...
    1717 images available.
    Please pick one of the available options:
     [0] name
     [1] owner_id
     [2] architecture
     [3] type
     [4] virtualization_type
     
     > 2
     Please pick one of the available options:
      [0] x86_64
      [1] i386

     > 0
     577 images available.
     Please pick one of the available options:
      [0] name
      [1] owner_id
      [2] architecture
      [3] type
      [4] virtualization_type

     > 3
     Please pick one of the available options:
      [0] machine
      [1] kernel
      [2] ramdisk

     > 0
     519 images available.
     Please pick one of the available options:
      [0] name
      [1] owner_id
      [2] architecture
      [3] type
      [4] virtualization_type

     > 4
     Please pick one of the available options:
      [0] hvm
      [1] paravirtual

     > 1
     386 images available.
     Please pick one of the available options:
      [0] name
      [1] owner_id
      [2] architecture
      [3] type
      [4] virtualization_type

     > 0
     Please pick one of the available options:
      [0] Ubuntu 10.10 64-bit Server Python Erlang Java
      [1] RightImage_Ubuntu_8.04_x64_v5.5.9.1_EBS
      ...
      [383] ubuntu-9.10-karmic-server-amd64-20100121
      [384] xarch-core-image
      [385] radiant-0.9.1_64_0.2_ami-75d4e101

     > 385
     Image selected: radiant-0.9.1_64_0.2_ami-75d4e101
     Image:ami-033d0977
     
# Requirements

In order to use `ec2selector` you need login credentials to Amazon EC2.
You can either pass these credentials to EC2Selector, e.g.:

    from ec2selector import EC2Selector
    EC2Selector().select(access_key='AKIA...', secret_key='xWD3...')

or you can set them in environment variables, e.g.:

    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIA...'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'xWD3...'

If you don't specify them, the interactive prompt will ask for them.

# Motivation

`ec2selector` is based on [boto](https://github.com/boto/boto), a great Python 
library to interact with Amazon EC2 instances. The only way to select an AMI 
with boto is by specifying its image ID. `ec2selector` expands this behavior by
letting you pick an image based on its attributes, not on its ID.

# Installing

    pip install ec2selector

# Contributing

1. fork and clone the project
2. install the dependencies above
3. run the tests with `python tests.py`
4. hack at will
5. commit and push
6. send a pull request

# License

See LICENSE.txt