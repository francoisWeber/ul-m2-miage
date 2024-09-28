# see sample https://github.com/vespa-engine/sample-apps/tree/master/commerce-product-ranking 
vespa config set target local
vespa status deploy --wait 10 && vespa deploy --wait 200 .
