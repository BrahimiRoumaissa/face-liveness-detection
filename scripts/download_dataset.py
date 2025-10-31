"""
Dataset Download Helper Script
Downloads and prepares datasets for face liveness detection training
"""
import os
import requests
import zipfile
import tarfile
from pathlib import Path
import argparse


def download_file(url, destination):
    """Download a file with progress bar"""
    print(f"Downloading from {url}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)
    print("\nDownload complete!")


def extract_archive(archive_path, extract_to):
    """Extract zip or tar archive"""
    print(f"Extracting {archive_path}...")
    extract_to = Path(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)
    
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tar'):
        with tarfile.open(archive_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_to)
    
    print(f"Extracted to {extract_to}")


def organize_casia_fasd(source_dir, target_dir):
    """Organize CASIA-FASD dataset structure"""
    print("Organizing CASIA-FASD dataset...")
    source = Path(source_dir)
    target = Path(target_dir)
    
    target_real = target / "real"
    target_spoof = target / "spoof"
    target_real.mkdir(parents=True, exist_ok=True)
    target_spoof.mkdir(parents=True, exist_ok=True)
    
    # CASIA-FASD structure: train_release/ or test_release/
    for subdir in ['train_release', 'test_release']:
        train_dir = source / subdir
        if not train_dir.exists():
            continue
            
        for folder in train_dir.iterdir():
            if not folder.is_dir():
                continue
                
            folder_name = folder.name.lower()
            
            # Copy based on folder name
            if '1' in folder_name or 'real' in folder_name or 'live' in folder_name:
                # Real faces
                for img in folder.glob("*.jpg"):
                    target_real.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy(img, target_real / img.name)
            elif '2' in folder_name or '3' in folder_name or 'attack' in folder_name:
                # Spoof faces
                for img in folder.glob("*.jpg"):
                    target_spoof.mkdir(parents=True, exist_ok=True)
                    import shutil
                    shutil.copy(img, target_spoof / img.name)


def organize_replay_attack(source_dir, target_dir):
    """Organize Replay-Attack dataset structure"""
    print("Organizing Replay-Attack dataset...")
    source = Path(source_dir)
    target = Path(target_dir)
    
    target_real = target / "real"
    target_spoof = target / "spoof"
    target_real.mkdir(parents=True, exist_ok=True)
    target_spoof.mkdir(parents=True, exist_ok=True)
    
    import shutil
    
    # Replay-Attack structure: train/ or test/
    for split in ['train', 'test']:
        split_dir = source / split
        if not split_dir.exists():
            continue
            
        for folder in split_dir.iterdir():
            if not folder.is_dir():
                continue
                
            folder_name = folder.name.lower()
            
            if 'real' in folder_name or 'live' in folder_name:
                for img in folder.glob("*.jpg"):
                    shutil.copy(img, target_real / f"{split}_{img.name}")
            elif 'attack' in folder_name or 'spoof' in folder_name:
                for img in folder.glob("*.jpg"):
                    shutil.copy(img, target_spoof / f"{split}_{img.name}")


def main():
    parser = argparse.ArgumentParser(description='Download and prepare face liveness datasets')
    parser.add_argument('--dataset', choices=['casia', 'replay', 'celeba'], 
                       help='Dataset to download (casia, replay, or celeba)')
    parser.add_argument('--source-dir', type=str, 
                       help='Directory containing downloaded dataset')
    parser.add_argument('--target-dir', type=str, default='datasets',
                       help='Target directory for organized dataset')
    
    args = parser.parse_args()
    
    if args.dataset == 'casia':
        print("=" * 60)
        print("CASIA-FASD Dataset Setup")
        print("=" * 60)
        print("\n1. Download CASIA-FASD from:")
        print("   http://www.cbsr.ia.ac.cn/english/CASIA-FASD.asp")
        print("2. Extract the downloaded file")
        print("3. Run this script with:")
        print("   python scripts/download_dataset.py --dataset casia --source-dir <extracted_path>")
        
        if args.source_dir:
            organize_casia_fasd(args.source_dir, args.target_dir)
            print(f"\nDataset organized in {args.target_dir}/")
            print(f"Real images: {len(list((Path(args.target_dir) / 'real').glob('*.jpg')))}")
            print(f"Spoof images: {len(list((Path(args.target_dir) / 'spoof').glob('*.jpg')))}")
    
    elif args.dataset == 'replay':
        print("=" * 60)
        print("Replay-Attack Dataset Setup")
        print("=" * 60)
        print("\n1. Download Replay-Attack from:")
        print("   https://www.idiap.ch/en/dataset/replayattack")
        print("2. Extract the downloaded file")
        print("3. Run this script with:")
        print("   python scripts/download_dataset.py --dataset replay --source-dir <extracted_path>")
        
        if args.source_dir:
            organize_replay_attack(args.source_dir, args.target_dir)
            print(f"\nDataset organized in {args.target_dir}/")
            print(f"Real images: {len(list((Path(args.target_dir) / 'real').glob('*.jpg')))}")
            print(f"Spoof images: {len(list((Path(args.target_dir) / 'spoof').glob('*.jpg')))}")
    
    elif args.dataset == 'celeba':
        print("=" * 60)
        print("CelebA-Spoof Dataset Setup")
        print("=" * 60)
        print("\n1. Download CelebA-Spoof from:")
        print("   https://mmlab.ie.cuhk.edu.hk/projects/CelebA_Spoof.html")
        print("2. Note: This dataset requires registration and approval")
        print("3. After downloading, organize images into:")
        print("   datasets/real/")
        print("   datasets/spoof/")
        print("\nThe dataset structure should be:")
        print("datasets/real/*.jpg")
        print("datasets/spoof/*.jpg")


if __name__ == "__main__":
    main()

