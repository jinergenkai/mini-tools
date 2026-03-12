import {
  Circle,
  Twitter,
  Linkedin,
  Github,
  Facebook,
  Logo
} from "@/components/modules/icon.module";
import {
  Button,
  Input
} from "@/components/modules/shadcn.module";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-50 dark:bg-gray-900 pt-16 pb-12 border-t border-gray-200 dark:border-gray-800">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-12">
          {/* Logo and Short Description */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Logo/>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
              Empowering businesses with intelligent AI solutions that drive innovation,
              efficiency, and growth in the digital age.
            </p>
            <div className="flex space-x-4">
              <Button variant="ghost" size="icon" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                <Twitter className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                <Linkedin className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                <Github className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                <Facebook className="h-5 w-5" />
              </Button>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-lg mb-4">Quick Links</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">About Us</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Services</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Case Studies</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Pricing</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Contact</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold text-lg mb-4">Resources</h3>
            <ul className="space-y-3">
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Blog</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Documentation</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">FAQ</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Support</a></li>
              <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">Developers</a></li>
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h3 className="font-semibold text-lg mb-4">Subscribe</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Stay updated with our latest AI innovations and industry insights.
            </p>
            <div className="flex space-x-2">
              <Input 
                placeholder="Your email" 
                className="bg-white dark:bg-gray-800" 
              />
              <Button className="bg-futureBlue hover:bg-futureBlue/90 text-white">
                Subscribe
              </Button>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-gray-200 dark:border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              © {currentYear} Agentic Vision AI. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-sm text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                Privacy Policy
              </a>
              <a href="#" className="text-sm text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                Terms of Service
              </a>
              <a href="#" className="text-sm text-gray-600 dark:text-gray-400 hover:text-futureBlue dark:hover:text-futureBlue">
                Cookie Policy
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;