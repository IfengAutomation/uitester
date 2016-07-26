import os

import subprocess

import shutil
import zipfile


class GradleBuilder:

    """docstring for GradleBuilder"""

    def __init__(self, project_path):
        super(GradleBuilder, self).__init__()
        self.projectPath = project_path
        self.gradlew = os.path.join(project_path, 'gradlew')

    def androidTest(self):
        outputDir = os.path.join(self.projectPath, 'app/build/outputs/apk')
        if os.path.exists(outputDir):
            # print outputDir
            out_apks = os.listdir(outputDir)
            print('GradleBuilder: clear out put')
            for apk in out_apks:
                os.remove(os.path.join(outputDir, apk))
        # build test apk
        print('GradleBuilder: build from %s' % (self.gradlew,))
        cmd = '%s assembleDebugAndroidTest -p %s' % (self.gradlew, self.projectPath)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

        out_apks = os.listdir(outputDir)
        for apk in out_apks:
            apk_path = os.path.join(outputDir, apk)
            moved_apk_path = os.path.join(os.getcwd(), apk)
            shutil.copy(apk_path, moved_apk_path)
            return moved_apk_path


class Signer:

    """
    Signer
    Use jarsigner to resign apk
    """

    def __init__(self):
        super(Signer, self).__init__()

    def is_signed(self, apk):
        pass

    def sign(self, apk, keystore, password):
        if not os.path.exists(apk):
            print('Signer: not found target. ' + apk)
            return
        if not zipfile.is_zipfile(apk):
            print('Signer: target is not a zip file. ' + apk)
            return
        abs_path = os.path.abspath(apk)
        base_name = abs_path[:len(abs_path) - 4]
        tmp_dir = base_name + '_tmp'
        output = base_name + '-unsigned.apk'

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.mkdir(tmp_dir)
        origin_file = zipfile.ZipFile(apk)
        origin_file.extractall(path=tmp_dir)
        origin_file.close()

        # remove META-INF in ziped file
        shutil.rmtree(tmp_dir + '/META-INF')

        targetFile = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(tmp_dir):
            for filename in filenames:
                targetFile.write(os.path.join(dirpath, filename), os.path.join(dirpath[len(tmp_dir):], filename))
        targetFile.close()

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        # resgin zip file
        signerCmd = 'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore %s %s %s' % (
            keystore, output, 'at-release')
        if password is not None and password != '':
            signerCmd = signerCmd + ' -storepass ' + password
        os.system(signerCmd)

        newName = base_name + '_signed.apk'
        if os.path.exists(newName):
            os.remove(newName)
        os.rename(output, newName)
        return newName