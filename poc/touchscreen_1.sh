#!/bin/bash
evtest /dev/input/event0 | head -1 >> /dev/null
