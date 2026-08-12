#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

case "$(uname -m)" in
  x86_64|amd64)
    target=x86_64-unknown-linux-gnu
    ;;
  aarch64|arm64)
    target=aarch64-unknown-linux-gnu
    ;;
  *)
    echo "linux-computer-use: unsupported architecture: $(uname -m)" >&2
    exit 64
    ;;
esac

backend="$script_dir/computer-use-linux-$target"
helper="$script_dir/computer-use-linux-cosmic-$target"

if [ ! -x "$backend" ]; then
  echo "linux-computer-use: missing executable backend: $backend" >&2
  exit 66
fi

if [ -x "$helper" ]; then
  export COMPUTER_USE_LINUX_COSMIC_HELPER="$helper"
fi

exec "$backend" "$@"
