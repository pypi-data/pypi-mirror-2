from pyxnat.xuri import *


def test_is_related():
    assert \
        is_related( '/REST/projects/Volatile/subjects/01/files/1.nii.gz',
                    '/REST/projects/Volatile/subjects/01/resources/09808/files'
                  )

    assert \
        is_related( '/REST/projects/Volatile/subjects/01/resources/09808/files',
                    '/REST/projects/Volatile/subjects/01/files/1.nii.gz'
                  )

    assert not \
        is_related( '/REST/projects/Volatile/subjects/01/files/1.nii.gz',
                    '/REST/projects/Volatile/resources/098089/files'
                  )

    assert \
        is_related( '/REST/projects/Volatile/subjects/01/files/1.nii.gz',
                    '/REST/projects/Volatile/subjects/01/files/1.nii.gz'
                  )

    assert \
        is_related( '/REST/projects/Volatile/subjects/01',
                    '/REST/projects/Volatile/subjects'
                  )

    assert not \
        is_related( '/REST/projects/Test/subjects/01',
                    '/REST/projects/Volatile/subjects'
                  )


