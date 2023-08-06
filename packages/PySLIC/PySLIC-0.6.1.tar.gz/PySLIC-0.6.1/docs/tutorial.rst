==========================================
PySLIC TUTORIAL
==========================================

CONVENTIONS
-----------

 + Functions that use random numbers take a parameter R which can be used to initialise
        random numbers. See utils.get_random for details.
 + Arguments should not be modified unless expected (and stated in __doc__ string)

IMAGE TYPE
----------

The Image type (pyslic.Image) is the basic type of pyslic.

Lazy Loading
~~~~~~~~~~~~

Image uses lazy loading. You create images by simply giving them paths to image files, but the images are
not loaded into memory until necessary. This is necessary to support large collections of images (which cannot be
held simultaneously in memory).

For example, to load a directory full of images:

::

	pat=re.compile('images-directory/([A-Za-z]+)-[0-9]+.jpg')
	imgs=[]
	for F in glob('images-directory/*.jpg'):
		img=Image()
		match=pat.match(F)
		img.label=match.group(1)
		img.channels['protein']=F
		imgs.append(img)

This creates a list *imgs* where each element is an image.


COMPUTING FEATURES
------------------

There are two ways to compute features:

	* Through computefeatures()
	* Calling individual functions

The first method uses an image class, which contains the paths to the files.

The individual functions take preprocessed images of the protein, of the DNA channel, or of the residual fluorescence. Check their individual documentation for details.

USING COMPUTEFEATURES
~~~~~~~~~~~~~~~~~~~~~

::

    from pyslic import Image, computefeatures

    image=Image()
    # Set up the image
    image.channels[Image.protein_channel]='/images/image-prot.png'
    image.channels[Image.dna_channel]='/images/image-dna.png'
    image.channels[Image.crop_channel]='/images/image-crop.png'

    F=computefeatures(image,'mcell')
    image.unload() # Save memory


You can also compute features for a large collection of images:

::

    imgs = loadimgs()
    features = computefeatures(imgs,'slf7dna')

CLASSIFICATION
----------------

Besides feature calculation, the next biggest module of PySLIC is the classification module. It contains a small set of classifiers, feature normalisation and selection functions, and other utility functions.

Once you have your features and labels and want to test classification accuracy, you can just call *nfoldcrossvalidation()*:

::

    cmatrix, names = nfoldcrossvalidation(features,labels)

This will perform 10-fold cross-validation using a default classifier. cmatrix will be a confusion matrix, so that cmatrix[i,j] corresponds to the number of times that an element of class i was classified as being of class j. To map these indices back to your labels, use the *names* vector.

Classifiers
~~~~~~~~~~~

Classifiers are objects which support at least two methods: *train()* and *apply()*. For example:

::

    classif = defaultClassifier()
    classif.train(trainfeats,trainlabels)

    output = classif.apply(testfeats)

The default classifier does a feature normalisation (to [-1,+1] interval) followed by *stepwise discriminant analysis* (SDA) for feature selection and then performs a grid-search for the parameters of a libSVM-based classifier with an RBF kernel.


