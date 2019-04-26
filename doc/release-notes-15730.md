RPC changes
-----------
The RPC `getwalletinfo` response now includes the `scanning` key with an object
if a scan is in progress, `false` otherwise. Currently the object has the
scanning duration and progress.
