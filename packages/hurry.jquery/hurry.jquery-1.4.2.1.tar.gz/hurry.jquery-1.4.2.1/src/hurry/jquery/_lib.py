from hurry.resource import Library, ResourceInclusion

jquery = Library('jquery')

jquery = ResourceInclusion(jquery, 'jquery-1.4.2.js', minified='jquery-1.4.2.min.js')