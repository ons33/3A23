<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class ProductController extends AbstractController
{
    #[Route('/product', name: 'app_product')]
    public function index(): Response
    {
        $price= 20;
        $products =[1,2,3];
        return $this->render('product/index.html.twig', 
        [
             'price1' => $price, 
             'prod' => $products 
        ]);
    }
}
