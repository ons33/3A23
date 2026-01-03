<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class Service2Controller extends AbstractController
{
    #[Route('/service2/{id}', name: 'app_service2')]
    public function index($id): Response
    {
        // 😎✨🚀🐍💻🔍📝🎯✅🔥
        return $this->render('service2/index.html.twig', [
            'controller_name' => 'Service2Controller',
        ]);
    }
}
